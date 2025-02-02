import os
import tomllib
import subprocess
import toml


if __name__ == "__main__":
    # Ensure that pyproject file exists
    if not os.path.isfile("pyproject.toml"):
        raise Exception("Missing pyproject.toml")

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        version: str = data["project"]["version"]
        [major, minor, patch] = [int(p) for p in version.split(".")]
        diff = [0, 0, 0]
        print(f"Current version: {version}")
        while True:
            publish_type = input("1 - Major, 2 - Minor, 3 - Patch: ")
            if not publish_type.isdigit() or int(publish_type) not in {1, 2, 3}:
                print("Select 1 - Major, 2 - Minor, or 3 - Patch only")
                continue
            diff[int(publish_type) - 1] = 1
            [new_major, new_minor, new_patch] = [
                major + diff[0],
                minor + diff[1],
                patch + diff[2],
            ]
            confirmation = input(
                f"Next version: {new_major}.{new_minor}.{new_patch}. Are you sure? (Y/n) "
            )
            if confirmation != "Y" and confirmation != "y":
                print("Aborting publish")
                break

            data["project"]["version"] = f"{new_major}.{new_minor}.{new_patch}"
            with open("pyproject.toml", "w") as writing_f:
                toml.dump(data, writing_f)

            break
