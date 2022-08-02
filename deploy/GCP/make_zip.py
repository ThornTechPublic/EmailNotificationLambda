if __name__ == "__main__":
    from zipfile import ZipFile
    from os import chdir, walk
    from os.path import join, split

    chdir(join(split(__file__)[0], "..", ".."))

    with ZipFile(join("deploy", "GCP", "emailAlertGoogleArchive.zip"), "w") as zf:
        zf.write(join("deploy", "GCP", "main.py"), "main.py")
        zf.write(join("src", "main", "GCP", "requirements.txt"), "requirements.txt")
        zf.write(join("src", "main", "GCP", "google_handler.py"), "google_handler.py")
        for directory, dirs, filenames in walk(join("src", "main", "res")):
            for file in filenames:
                zf.write(join(directory, file))
        zf.write(join("src", "main", "__init__.py"))
        zf.write(join("src", "__init__.py"))
