from utils.hash import sha256_hash
import shutil
import os
import sys
import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Manage models in a directory.")
    parser.add_argument("action", choices=[
                        "add", "remove"], help="Action to perform: 'add' or 'remove' a model.")
    parser.add_argument("-p", "--filepath", metavar="FILEPATH",
                        type=str, help="Filepath of the model.")
    args = parser.parse_args()
    if not args.filepath:
        parser.error("Please provide a filepath.")
    filepath = args.filepath
    print(filepath)
    modelzoo_location = os.path.dirname(os.path.realpath(sys.argv[0]))

    if not os.path.exists(args.filepath):
        raise FileNotFoundError('No model found in {filepath}.')
    if not os.path.exists(os.path.join(modelzoo_location, 'models.json')):
        raise FileNotFoundError(
            f'No models.json found in {os.path.join(modelzoo_location,"models.json")} which is required.')

    with open(os.path.join(modelzoo_location, 'models.json'), 'r') as f:
        models = json.load(f)

    if args.action == "add":
        print(f"\nAdding model from {filepath} to the directory.")
        # add to model.json
        model_name = os.path.basename(filepath).split('.pt')[0]
        model_hash = sha256_hash(filepath)
        models[model_name] = model_hash
        with open(os.path.join(modelzoo_location, 'models.json'), 'w') as f:
            json.dump(models, f)
        # move model to model directory

        destination_path = os.path.join(
            modelzoo_location, 'models', os.path.basename(filepath))
        try:
            shutil.copy(filepath, destination_path)
            print(f"File copied successfully to {destination_path}.")
        except PermissionError:
            print(
                "Error: Permission denied. Make sure you have the necessary permissions.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif args.action == "remove":
        print(f"\nRemoving model from the directory: {filepath}.")
        # remove from model.json
        model_name = os.path.basename(filepath).split('.pt')[0]
        if model_name in models.keys():
            del models[model_name]
            with open(os.path.join(modelzoo_location, 'models.json'), 'w') as f:
                json.dump(models, f)
        # delete model from folder
        try:
            os.remove(filepath)
            print(
                f"File removed successfully from {os.path.dirname(filepath)}.")
        except Exception as e:
            print(f"An error occured: {e}")


if __name__ == "__main__":
    main()
