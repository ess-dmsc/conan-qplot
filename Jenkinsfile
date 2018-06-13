project = "conan-qplot"

conan_remote = "ess-dmsc-local"
conan_user = "ess-dmsc"
conan_pkg_channel = "stable"

remote_upload_node = "ubuntu1804"

images = [
  'ubuntu1804': [
    'name': 'essdmscdm/ubuntu18.04-build-node:1.1.0',
    'sh': 'sh'
  ]
]

base_container_name = "${project}-${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

if (conan_pkg_channel == "stable") {
  if (env.BRANCH_NAME != "master") {
    error("Only the master branch can create a package for the stable channel")
  }
  conan_upload_flag = "--no-overwrite"
} else {
  conan_upload_flag = ""
}

def get_pipeline(image_key) {
  return {
    node('docker') {
      def container_name = "${base_container_name}-${image_key}"
      try {
        def image = docker.image(images[image_key]['name'])
        def custom_sh = images[image_key]['sh']
        def container = image.run("\
          --name ${container_name} \
          --tty \
          --cpus=2 \
          --memory=4GB \
          --network=host \
          --env http_proxy=${env.http_proxy} \
          --env https_proxy=${env.https_proxy} \
          --env local_conan_server=${env.local_conan_server} \
        ")

        stage("${image_key}: Checkout") {
          sh """docker exec ${container_name} ${custom_sh} -c \"
            git clone \
              --branch ${env.BRANCH_NAME} \
              https://github.com/ess-dmsc/${project}.git
          \""""
        }  // stage

        stage("${image_key}: Conan setup") {
          withCredentials([
            string(
              credentialsId: 'local-conan-server-password',
              variable: 'CONAN_PASSWORD'
            )
          ]) {
            sh """docker exec ${container_name} ${custom_sh} -c \"
              set +x
              conan remote add \
                --insert 0 \
                ${conan_remote} ${local_conan_server} && \
              conan user \
                --password '${CONAN_PASSWORD}' \
                --remote ${conan_remote} \
                ${conan_user} \
                > /dev/null
            \""""
          }  // withCredentials
        }  // stage

        stage("${image_key}: Package") {
          sh """docker exec ${container_name} ${custom_sh} -c \"
            cd ${project}
            conan create . ${conan_user}/${conan_pkg_channel} \
              --settings qplot:build_type=Release \
              --options qplot:shared=False \
              --build=outdated
          \""""

          // Use shell script to avoid escaping issues
          pkg_name_and_version = sh(
            script: """docker exec ${container_name} ${custom_sh} -c \"
                cd ${project} &&
                ./get_conan_pkg_name_and_version.sh
              \"""",
            returnStdout: true
          ).trim()
        }  // stage

        /*
        stage("${image_key}: Local upload") {
          sh """docker exec ${container_name} ${custom_sh} -c \"
            conan upload \
              --all \
              ${conan_upload_flag} \
              --remote ${conan_remote} \
              ${pkg_name_and_version}@${conan_user}/${conan_pkg_channel}
          \""""
        }  // stage

        // Upload to remote repository only once
        if (image_key == remote_upload_node) {
          stage("${image_key}: Remote upload") {
            withCredentials([
              usernamePassword(
                credentialsId: 'cow-bot-bintray-username-and-api-key',
                passwordVariable: 'COWBOT_PASSWORD',
                usernameVariable: 'COWBOT_USERNAME'
              )
            ]) {
              sh """docker exec ${container_name} ${custom_sh} -c \"
                set +x
                conan user \
                  --password '${COWBOT_PASSWORD}' \
                  --remote ess-dmsc \
                  ${COWBOT_USERNAME} \
                  > /dev/null
              \""""
            }  // withCredentials

            sh """docker exec ${container_name} ${custom_sh} -c \"
              conan upload \
                ${conan_upload_flag} \
                --remote ess-dmsc \
                ${pkg_name_and_version}@${conan_user}/${conan_pkg_channel}
            \""""
          }  // stage
        }  // if
        */
      } finally {
        sh "docker stop ${container_name}"
        sh "docker rm -f ${container_name}"
      }  // finally
    }  // node
  }  // return
}  // def

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

        /*
        stage("macOS: Upload") {
          sh "conan upload \
            --all \
            ${conan_upload_flag} \
            --remote ${conan_remote} \
            ${pkg_name_and_version}@${conan_user}/${conan_pkg_channel}"
        }  // stage
        */
      }  // dir
    }  // node
  }  // return
}  // def


node {
  checkout scm

  def builders = [:]
  for (x in images.keySet()) {
    def image_key = x
    builders[image_key] = get_pipeline(image_key)
  }
  builders['macOS'] = get_macos_pipeline()
  parallel builders

  // Delete workspace when build is done.
  cleanWs()
}
