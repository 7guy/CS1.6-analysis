import os
import shutil
import subprocess
import argparse


def add_plugin(sma_file):
    # Define paths
    scripts_dir = r'C:\Program Files (x86)\Valve\Counter-Strike\cstrike\addons\amxmodx\scripting'
    compiled_dir = r'C:\Program Files (x86)\Valve\Counter-Strike\cstrike\addons\amxmodx\scripting\compiled'
    plugins_dir = r'C:\Program Files (x86)\Valve\Counter-Strike\cstrike\addons\amxmodx\plugins'
    config_file = r'C:\Program Files (x86)\Valve\Counter-Strike\cstrike\addons\amxmodx\configs\plugins.ini'
    compile_exe = r'C:\Program Files (x86)\Valve\Counter-Strike\cstrike\addons\amxmodx\scripting\compile.exe'

    # Copy the .sma file to the scripts directory
    try:
        shutil.copy(sma_file, scripts_dir)
        print(f"Copied {sma_file} to {scripts_dir}")
    except Exception as e:
        print(f"Error copying {sma_file}: {e}")
        return

    # Compile the .sma file
    try:
        print("Compilation process started")
        subprocess.run([compile_exe], cwd=scripts_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        return

    # Get the plugin name from the .sma file
    plugin_name = os.path.basename(sma_file).replace('.sma', '.amxx')
    compiled_plugin = os.path.join(compiled_dir, plugin_name)

    # Check if the plugin was successfully compiled
    if not os.path.exists(compiled_plugin):
        print(f"Compilation failed. {plugin_name} not found.")
        return

    # Move the compiled plugin to the plugins directory
    try:
        shutil.copy(compiled_plugin, plugins_dir)
        print(f"Moved {plugin_name} to {plugins_dir}")
    except Exception as e:
        print(f"Error moving {plugin_name}: {e}")
        return

    # Add the plugin name to config.ini
    try:
        with open(config_file, 'a') as config:
            config.write(f"\n{plugin_name}")
        print(f"Added {plugin_name} to {config_file}")
    except Exception as e:
        print(f"Error updating {config_file}: {e}")
        return


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Add AMXX plugin to Counter-Strike game")
    parser.add_argument('-f', '--file', required=True,
                        help="The name of the .sma plugin file (with or without the full path)")

    # Parse the arguments
    args = parser.parse_args()

    # Construct the full path if the user didn't provide a full path
    sma_file = args.file
    if not os.path.isabs(sma_file):
        sma_file = os.path.expanduser(f"~/PycharmProjects/cs_analytics/utils/amx plugins/{sma_file}")

    # Add the plugin
    add_plugin(sma_file)


if __name__ == "__main__":
    # ===== python utils/add_plugin.py -f hi.sma
    main()


