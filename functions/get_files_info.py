import os

from dotenv.main import StrPath


def get_files_info(working_directory: StrPath, directory: StrPath = ".") -> str:
    try:
        current_path = os.path.join(working_directory, directory)
        current_abspath = os.path.abspath(current_path)

        # print(current_path)
        # print(current_abspath)

        report = f"Result for {'current' if directory == '.' else str(directory)} directory:\n"

        if not current_abspath.startswith(os.path.abspath(working_directory)):
            report += f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
            return report

        if not os.path.isdir(current_abspath):
            report += f'\tError: "{directory}" is not a directory'
            return report

        files = os.listdir(current_path)

        for file in files:
            if file.startswith("__"):
                continue
            file_path = os.path.join(current_path, file)
            report += f" - {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"

    except Exception as error:
        return f"Error: {error}"
    return report
