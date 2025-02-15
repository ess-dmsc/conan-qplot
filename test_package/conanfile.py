from conans import ConanFile, CMake, tools
import os

class qplotTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')
        self.copy("*.a", dst="bin", src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run("objdump -s -j .note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt6Core.so.6.2.4")
            self.run("ldd `which qmake6`")
            self.run("strip -v --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt6*.so.?.?.?")
            self.run("ldd `which qmake6`")
            self.run(".%sexample -platform offscreen" % os.sep)
