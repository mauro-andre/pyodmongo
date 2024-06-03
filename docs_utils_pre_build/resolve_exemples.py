from pathlib import Path
import os


class Replace:
    _exemples_folder = Path().absolute() / "docs_utils_pre_build" / "examples"

    def __init__(self, folder_path: Path) -> None:
        self.folder_path: Path = folder_path

    def _all_exemples(self):
        return list(
            filter(lambda x: x.endswith(".py"), os.listdir(self._exemples_folder))
        )

    def _all_md_files_on_folder(self):
        return list(filter(lambda x: x.endswith(".md"), os.listdir(self.folder_path)))

    def resolve_replace(self):
        file_names = self._all_md_files_on_folder()
        examples = self._all_exemples()
        for file_name in file_names:
            file_path: Path = self.folder_path / file_name
            with open(file=file_path, mode="r+", encoding="utf-8") as md_file:
                current_md_content = md_file.read()
                for exemple_name in examples:
                    exemple_path: Path = self._exemples_folder / exemple_name
                    with open(file=exemple_path, mode="r", encoding="utf-8") as py_file:
                        content_py = py_file.read()
                        current_md_content = current_md_content.replace(
                            f"__{exemple_name}__", content_py
                        )
                md_file.seek(0)
                md_file.write(current_md_content)
                md_file.truncate()


en_folder_path = Path().absolute() / ".docs_tmp" / "en"
pt_folder_path = Path().absolute() / ".docs_tmp" / "pt-BR"

en_obj = Replace(folder_path=en_folder_path)
pt_obj = Replace(folder_path=pt_folder_path)

en_obj.resolve_replace()
pt_obj.resolve_replace()
