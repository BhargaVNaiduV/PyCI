from urllib.request import urlopen
import json, time
import os,subprocess


waitsec = 10



def main():
    commit=''
    while True:
        oldcommit=commit
        commit = get_latest_commit('BhargaVNaiduV', 'publisher')
        if oldcommit != '' and commit != oldcommit:
            print('***** NEW COMMIT ******')
            try:
                build_docker_image()
                break
            except Exception as e:
                print(e)
        print('last commit: %s' % commit['html_url'])
        time.sleep(waitsec)
        
def run_tests(scriptname,path):
    # this module is used used to run any tests that we can do on source code before building image 
    os.chdir(path)
    name_of_test_script,path= scriptname,path
    try:
        subprocess.run(["python", "-m", "unittest",scriptname], check=True)

    except Exception as e:
        print("exception occured when ruiing tests{e}")    
    

def build_docker_image():
    git_repo_url = "git@github.com:BhargaVNaiduV/publisher.git"
    clone_directory = "/home/bhargav/lambda_publisher_function/publisher/test_dir1"
    docker_image_name = "publisher_auto"
    try:
    # Check if the clone directory exists, if not, create it
        if not os.path.exists(clone_directory):
            os.makedirs(clone_directory)

    # Run the git clone command
        subprocess.run(["git", "clone", git_repo_url, clone_directory], check=True)
        print("Git clone successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git clone: {e}")
        exit(1)

    try:
    # Change the current working directory to the cloned repository
        os.chdir(clone_directory)

        # Run the docker build command
        subprocess.run(["docker", "build", "-t", docker_image_name, "."], check=True)
        print("Docker image build successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Docker image build: {e}")
        exit(1)

def get_latest_commit(owner, repo, branch='main'):
    url = 'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1&sha={branch}'.format(
        owner=owner, repo=repo, branch=branch
    )
    response = urlopen(url).read()
    data = json.loads(response.decode())
    # print(data)
    return data[0] if data else None

if __name__ == '__main__':
    main()
