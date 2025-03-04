@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.ConanPackageBuilder

project = "conan-qplot"

conan_user = "ess-dmsc"
conan_pkg_channel = "stable"

container_build_nodes = [
  'centos'     : ContainerBuildNode.getDefaultContainerBuildNode('centos7-gcc11-qt6'),
  'ubuntu2204' : ContainerBuildNode.getDefaultContainerBuildNode('ubuntu2204-qt6')
]

package_builder = new ConanPackageBuilder(this, container_build_nodes, conan_pkg_channel)
package_builder.defineRemoteUploadNode('centos')

builders = package_builder.createPackageBuilders { container ->
  package_builder.addConfiguration(container, [
    'settings': [
      'qplot:build_type': 'Release'
    ],
    'options': [
      'qplot:shared': "False"
    ]
  ])

  package_builder.addConfiguration(container, [
    'settings': [
      'qplot:build_type': 'Debug'
    ],
    'options': [
      'qplot:shared': "False"
    ]
  ])
}

def get_macos_pipeline() {
  return {
    node('macos') {
      cleanWs()
      dir("${project}") {
        stage("macOS: Checkout") {
          checkout scm
        }  // stage

        stage("macOS: Package") {
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings qplot:build_type=Release \
            --options qplot:shared=False \
            --build=outdated"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings qplot:build_type=Debug \
            --options qplot:shared=False \
            --build=outdated"

          sh "conan info ."
        }  // stage
      }  // dir
    }  // node
  }  // return
}  // def


node {
  checkout scm

  if (env.ENABLE_MACOS_BUILDS.toUpperCase() == 'TRUE') {
    builders['macOS'] = get_macos_pipeline()
  }

  try {
    parallel builders
  } finally {
    cleanWs()
  }
}
