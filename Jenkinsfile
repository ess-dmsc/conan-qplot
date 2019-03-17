@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.ConanPackageBuilder

project = "conan-qplot"

conan_remote = "ess-dmsc-local"
conan_user = "ess-dmsc"
conan_pkg_channel = "testing"

container_build_nodes = [
  'centos': ContainerBuildNode.getDefaultContainerBuildNode('centos7'),
  'ubuntu': ContainerBuildNode.getDefaultContainerBuildNode('ubuntu1804')
]

package_builder = new ConanPackageBuilder(this, container_build_nodes, conan_pkg_channel)
package_builder.defineRemoteUploadNode('ubuntu1804')

builders = package_builder.createPackageBuilders { container ->
  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Release'
    ],
    'options': [
      'h5cpp:shared': "False"
    ]
  ])

  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Debug'
    ],
    'options': [
      'h5cpp:shared': "False"
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

        stage("macOS: Conan setup") {
          withCredentials([
            string(
              credentialsId: 'local-conan-server-password',
              variable: 'CONAN_PASSWORD'
            )
          ]) {
            sh "conan user \
              --password '${CONAN_PASSWORD}' \
              --remote ${conan_remote} \
              ${conan_user} \
              > /dev/null"
          }  // withCredentials
        }  // stage

        stage("macOS: Package") {
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings qplot:build_type=Release \
            --options qplot:shared=False \
            --build=outdated"

          pkg_name_and_version = sh(
            script: "./get_conan_pkg_name_and_version.sh",
            returnStdout: true
          ).trim()
        }  // stage

        stage("macOS: Upload") {
          sh "conan upload \
            --all \
            ${conan_upload_flag} \
            --remote ${conan_remote} \
            ${pkg_name_and_version}@${conan_user}/${conan_pkg_channel}"
        }  // stage
      }  // dir
    }  // node
  }  // return
}  // def


node {
  checkout scm

  builders['macOS'] = get_macos_pipeline()

  try {
    parallel builders
  } finally {
    cleanWs()
  }
}
