import json
import os
import shutil
from typing import Dict, Callable, Union, Any
import pickle

import numpy as np

import trainer.lib as lib

BINARIES_DIRNAME = "binaries"
JSON_MODEL_FILENAME = "json_model.json"
BINARY_TYPE_KEY = "binary_type"
PICKLE_EXT = 'pickle'


def build_full_filepath(name: str, dir_path: str):
    basename = os.path.splitext(name)[0]  # If a file ending is provided it is ignored
    return os.path.join(dir_path, f"{basename}.json")


def dir_is_json_class(dir_name: str, json_checker: Callable[[str], bool] = None):
    if json_checker is None:
        def json_checker(json_val: str) -> bool:
            return True
    # Check if the json exists:
    json_path = os.path.join(dir_name, JSON_MODEL_FILENAME)
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            json_content = json.load(f)
        if json_checker(json_content):
            return True
    # TODO Check other constraints (binaries)
    return False


class JsonClass:
    """
    Intended to be subclassed by classes which need to persist their state
    in the form of numpy binaries (Video, images...) and json metadata (name, attributes...).
    """

    def __init__(self, name: str, model: Dict = None, b_model: Dict = None):
        self.name = name
        self.binaries_dir_path = None

        if model is not None:
            self.json_model = model
        else:
            self.json_model = {}

        if b_model is not None:
            self._binaries_model = b_model
        else:
            self._binaries_model = {}
        self._binaries: Dict[str, np.ndarray] = {}

        self._last_used_parent_dir = None

    @classmethod
    def from_disk(cls, dir_path: str, pre_load_binaries=False):
        if not dir_is_json_class(dir_path):
            raise Exception(f"{dir_path} is not a valid directory.")

        name = os.path.basename(dir_path)

        full_file_path = os.path.join(dir_path, JSON_MODEL_FILENAME)
        with open(full_file_path, 'r') as f:
            json_content = json.load(f)
        res = cls(name, json_content["payload"], json_content["binaries"])
        res._last_used_parent_dir = os.path.dirname(dir_path)

        # Load binaries
        res.binaries_dir_path = os.path.join(dir_path, BINARIES_DIRNAME)
        if pre_load_binaries:
            binaries_paths_ls = os.listdir(res.binaries_dir_path)
            for binary_path in binaries_paths_ls:
                binary_name = os.path.splitext(os.path.basename(binary_path))[0]
                res.load_binary(binary_name)
        return res

    def load_binary(self, binary_id) -> None:
        path_no_ext = os.path.join(self.binaries_dir_path, binary_id)
        if self.get_binary_provider(binary_id) == lib.BinarySaveProvider.Pickle:
            with open(f'{path_no_ext}.{PICKLE_EXT}', 'rb') as f:
                binary_payload = pickle.load(f)
        else:
            binary_payload = np.load(f'{path_no_ext}.npy', allow_pickle=False)
        self._binaries[binary_id] = binary_payload

    def to_disk(self, dir_path: str = "", properly_formatted=True, prompt_user=False) -> None:
        if not dir_path:
            dir_path = self._last_used_parent_dir

        # Create the parent directory for this instance
        dir_path = os.path.join(dir_path, self.name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_name = os.path.join(dir_path, JSON_MODEL_FILENAME)
        self._last_used_parent_dir = os.path.dirname(dir_path)

        # Write the json model file
        with open(file_name, 'w+') as f:
            save_json = {
                "payload": self.json_model,
                "binaries": self._binaries_model
            }
            if properly_formatted:
                json.dump(save_json, f, indent=4)
            else:
                json.dump(save_json, f)

        # Write all binaries
        self.binaries_dir_path = os.path.join(dir_path, BINARIES_DIRNAME)
        if not os.path.exists(self.binaries_dir_path):
            os.mkdir(self.binaries_dir_path)
        for binary_key in self._binaries:
            self.save_binary(binary_key)

        if prompt_user:
            os.startfile(file_name)

    def get_binary_provider(self, binary_key: str):
        return lib.BinaryType.provider_map()[self._binaries_model[binary_key][BINARY_TYPE_KEY]]

    def save_binary(self, binary_key) -> None:
        """
        Writes the selected binary on disk.
        :param binary_key: ID of the binary
        """
        if self._last_used_parent_dir is None:
            raise Exception(f" Before saving {binary_key}, save {self.name} to disk!")
        if self.binaries_dir_path is None:
            self.binaries_dir_path = os.path.join(self._last_used_parent_dir, BINARIES_DIRNAME)
        path_no_ext = os.path.join(self.binaries_dir_path, binary_key)
        if self.get_binary_provider(binary_key) == lib.BinarySaveProvider.Pickle:
            with open(f'{path_no_ext}.{PICKLE_EXT}', 'wb') as f:
                pickle.dump(self._binaries[binary_key], f)
        else:
            np.save(path_no_ext, self._binaries[binary_key])

    def delete_on_disk(self, blocking=True):
        shutil.rmtree(self.get_working_directory(), ignore_errors=True)
        if blocking:
            while os.path.exists(self.get_working_directory()):
                pass

    def get_parent_directory(self):
        return self._last_used_parent_dir

    def get_working_directory(self):
        return os.path.join(self._last_used_parent_dir, self.name)

    def get_json_path(self):
        return os.path.join(self.get_working_directory(), JSON_MODEL_FILENAME)

    def add_binary(self,
                   binary_id: str,
                   binary: Union[Any, np.ndarray],
                   b_type: str = lib.BinaryType.Unknown.value,
                   meta_data=None,
                   overwrite=True) -> None:
        """
        Adds a numpy array or a pickled object.

        Note that the childclass must be saved using ```childclass.to_disk()``` to actually be written to disk.
        :param binary_id: Unique id of this binary
        :param binary: The binary content. Numpy Arrays and pickle-compatible objects are accepted.
        :param b_type:
        :param meta_data:
        :param overwrite: Overwrites existing binaries with the same id if true
        :return:
        """
        if not overwrite and binary_id in self._binaries:
            raise Exception("This binary already exists")
        self._binaries[binary_id] = binary

        self._binaries_model[binary_id] = {
            BINARY_TYPE_KEY: b_type
        }
        if meta_data is None:
            self._binaries_model[binary_id]["meta_data"] = {}
        else:
            self._binaries_model[binary_id]["meta_data"] = meta_data
        self.save_binary(binary_id)

    def remove_binary(self, binary_name):
        # Remove the numpy array from class and disk
        p = os.path.join(self.get_working_directory(), BINARIES_DIRNAME, f"{binary_name}.npy")
        os.remove(p)

        # Remove the key in model
        self._binaries_model.pop(binary_name)
        self._binaries.pop(binary_name)
        self.to_disk(self._last_used_parent_dir)

    def get_binary(self, binary_name):
        if binary_name not in self._binaries:
            self.load_binary(binary_name)
        return self._binaries[binary_name]

    def get_binary_model(self, binary_name):
        return self._binaries_model[binary_name]

    def get_binary_list_filtered(self, key_filterer: Callable[[Dict], bool]):
        return [i for i in self._binaries_model if key_filterer(self._binaries_model[i])]

    def get_image_stack_keys(self):
        return self.get_binary_list_filtered(lambda x: x["binary_type"] == lib.BinaryType.ImageStack.value)

    def count_binaries_memory(self):
        return sum([self._binaries[k].nbytes for k in self._binaries.keys()])

    def matplot_imagestacks(self):
        import matplotlib.pyplot as plt
        import seaborn as sns
        for binary in self._binaries_model:
            b = self._binaries[binary]
            btype = self._binaries_model[binary]["binary_type"]
            if btype == lib.BinaryType.ImageStack.value:
                # This is an image or a video
                b = b[0, :, :, :]
                if b.dtype == np.bool:
                    b = b.astype(np.float32) * 255.
                plt.title(binary)
                if b.shape[2] == 1:
                    # Grayscale is assumed
                    sns.heatmap(b[:, :, 0])
                else:
                    plt.imshow(b)
                plt.show()

    def __str__(self):
        res = f"Representation of {self.name}:\n"
        if self._last_used_parent_dir is not None:
            res += f"Last saved at {self.get_working_directory()}\n"
        res += f"Binaries: {len(self._binaries.keys())}\n"
        for binary in self._binaries.keys():
            res += f"{binary}: shape: {self._binaries[binary].shape} (type: {self._binaries[binary].dtype})\n"
            res += f"{json.dumps(self._binaries_model[binary], indent=4)}\n"
        res += json.dumps(self.json_model, indent=4)
        return res

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    parent_folder = 'C:\\Users\\rapha\\Desktop'
    read = False
    if read:
        example_class = JsonClass.from_disk(os.path.join(parent_folder, "jsonclass_example"))
    else:
        example_class = JsonClass("jsonclass_example", {})
        example_class.json_model["test_number"] = 4
        example_class.json_model["test_list"] = [1, 2, 3]
        example_class.json_model["test_dict"] = {"1": "3", "4": "8"}
        example_class.add_binary("test_image", np.ones((100, 100)))
        example_class.to_disk(parent_folder, prompt_user=True)
