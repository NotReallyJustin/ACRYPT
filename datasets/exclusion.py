def file_to_exclude():
    # Automatically generated library files that we shouldn't tamper with
    return [
        ".gitignore",
        "README.md",
        "LICENSE",
        "package.json",
        "package-lock.json",
        "Cargo.toml",
        "Pipfile",
        "Gemfile",
        "composer.json",
        "project.json",
        "pom.xml",
        "build.gradle"
    ]

def folders_to_exclude():
    return [
        "__pycache__",
        "node_modules",
        "Gemfile.lock",
        "vendor",
        "target",
        "build",
        ".git"
    ]