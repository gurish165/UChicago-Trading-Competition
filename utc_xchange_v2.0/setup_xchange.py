# setup_xchange.py -- sets up the environment for development of bots for the
# xChange platform. Also makes sure that the necessary dependencies (namely
# Python v3.7.0+) are installed

from __future__ import print_function
import subprocess
import sys
import os

if sys.version_info < (3, 7):
    version_str = ".".join(str(x) for x in sys.version_info[:3])
    print("Python version must be at least 3.7.0, is " + version_str)
    sys.exit(0)

import venv
from types import SimpleNamespace

done_msg = """
####################################################################################

\033[32;1mEverything is set up!\033[0m

You're set up and ready to start writing a bot for the UChicago Trading Competition!

To get started, you must first activate your Python virtual environment. You can
do this by using your terminal to run the command	

	\033[1m{}\033[0m

You should use this environment while developing your bot. To learn more about
virtual environment and how to use them, visit

	\033[4mhttps://docs.python.org/3/tutorial/venv.html\033[0m

Please consult the provided documentation for more info how to get started. Good
luck!"""

remote_exec_fix_msg = """
###################################################################################

\033[31;1mError: Please follow these instructions!\033[0m

Execution policy is too restrictive to use Python virtual environments.
To fix this, please open a PowerShell prompt as administrator and run:

    \033[1mSet-ExecutionPolicy -Scope CurrentUser RemoteSigned\033[0m

For details on why this is necessary, please visit:

    \033[4mhttps://www.stanleyulili.com/powershell/solution-to-running-scripts-is-disabled-on-this-system-error-on-powershell/\033[0m
    \033[4mhttps://tecadmin.net/powershell-running-scripts-is-disabled-system/\033[0m"""


class XChangeEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context):
        # type: (SimpleNamespace) -> None
        is_windows = sys.platform == "win32"

        if is_windows:
            python_exe = os.path.join(context.bin_path, "python.exe")
        else:
            python_exe = os.path.join(context.bin_path, "python")

        cmd = [python_exe, "-m", "pip", "install", "--upgrade"]
        cmd.extend(["pip", "setuptools"])

        # Install the packages necessary for running the provided code
        cmd.extend(
            [
                "betterproto",  # Interface with protobufs
                "numpy",  # Libraries for numerical computing / data manipulation
                "pandas",  # Greek
                "scipy",
                "pyyaml",  # Only necessary for casewriters, but conditional compilation is hard
            ]
        )

        subprocess.check_call(cmd)

        # Test if powershell execution policy allows for sourcing virtual env
        if is_windows:
            exec_policy = subprocess.run(
                "powershell Get-ExecutionPolicy", shell=True, capture_output=True
            )
            assert (
                exec_policy.returncode == 0
            ), "Unable to check execution policy for Powershell"

            policy = exec_policy.stdout.decode("utf-8").strip()
            if policy.lower() in ["default", "restricted", "undefined"]:
                print(remote_exec_fix_msg)
                sys.exit(1)


if __name__ == "__main__":

    if sys.platform == "win32":
        os.system("")  # Enables ANSI escape codes, somehow? Windows is so weird...

    XChangeEnvBuilder(
        symlinks=(os.name != "nt"),
        with_pip=True,
    ).create("venv")

    print(
        done_msg.format(
            ".\\venv\\Scripts\\activate"
            if sys.platform == "win32"
            else "source venv/bin/activate"
        )
    )
