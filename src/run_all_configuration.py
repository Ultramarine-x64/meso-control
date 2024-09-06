import os.path
import subprocess


def main():
    i = 1
    for configuration in [
        "./configurations/40_agents_vers1.json",
        "./configurations/40_agents_vers2.json",
        "./configurations/40_agents_vers3.json",
        "./configurations/40_agents_vers4.json",
        "./configurations/40_agents_vers5.json",
        "./configurations/40_agents_vers6.json"
    ]:
        if not os.path.exists(f"./result/{i}"):
            os.mkdir(f"./result/{i}")
        subprocess.call(
            [
                "python",
                "main.py",
                f"--configuration_file={configuration}",
                f"--path_to_results=./result/{i}",
                "--create_result_graph=True",
                "--create_step_images=False",
                "--create_gif=False"
            ]
        )
        i += 1


if __name__ == "__main__":
    main()
