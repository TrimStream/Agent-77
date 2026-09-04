import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        parts: list[str] = []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        if not stdout and not stderr:
            parts.append("No output produced")
        else:
            if stdout:
                parts.append(f"STDOUT: {stdout}")
            if stderr:
                parts.append(f"STDERR: {stderr}")

        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
