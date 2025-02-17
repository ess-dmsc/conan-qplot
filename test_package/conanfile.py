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
        # Test
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            # Hope this works now
            self.run(".%sexample -platform offscreen" % os.sep)
