import os
from conans import ConanFile, CMake, tools
from conans.util import files

class qplotConan(ConanFile):
    name = "qplot"
    version = "30469f8"
    license = "https://github.com/ess-dmsc/qplot/blob/master/LICENSE"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of qplot here>"
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
        self.run("cd qplot && git checkout 30469f8 && cd ..")

    def build(self):
        files.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake = CMake(self)
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            cmake.definitions["BUILD_STATIC_LIBS"] = "ON"
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
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["qplot"]
