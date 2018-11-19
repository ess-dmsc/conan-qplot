import os
from conans import ConanFile, CMake, tools
from conans.util import files

class qplotConan(ConanFile):
    name = "qplot"
    version = "933b38c"
    license = "https://github.com/ess-dmsc/qplot/blob/master/LICENSE"
    url = "https://bintray.com/ess-dmsc/qplot"
    description = "wrappers and convenience classes for custom plotting"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    # The folder name when the *.tar.gz release is extracted
    folder_name = "qplot"
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    def source(self):
        self.run("git clone https://github.com/ess-dmsc/qplot.git")
        self.run("cd qplot && git checkout 933b38c && cd ..")

    def build(self):
        files.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake = CMake(self)
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = ""

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_PREFIX_PATH"] = "/usr/local/opt/qt"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            # cmake.configure(source_dir="..", build_dir=".")
            self.run("cmake --debug-output %s %s" % ("..", cmake.command_line))
            cmake.build(build_dir=".")
            os.system("make install DESTDIR=./install")

    def package(self):
        self.copy("*", dst="include", src=self.build_dir+"/install/include")
        self.copy("*", dst="lib", src=self.build_dir+"/install/lib")
        self.copy("*", dst="lib64", src=self.build_dir+"/install/lib64")

    def package_info(self):
        self.cpp_info.libs = ["qplot"]
