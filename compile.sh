# ubuntu lts
# FROM ubuntu:20.04

sudo apt update
sudo DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
sudo apt install -y software-properties-common build-essential cmake git wget unzip
sudo apt install -y python3 python3-pip

# install Qt4
sudo apt-add-repository -y ppa:rock-core/qt4
sudo apt install -y qt4-default

sudo apt install -y libglew-dev freeglut3-dev libeigen3-dev libann-dev

cd /home/slongle/L1-Skeleton/PointCloud/depends/ANN
sudo wget https://github.com/jasonkena/L1-Skeleton/files/10715019/ann_1.1.2.zip
sudo unzip ann_1.1.2.zip
sudo mv ann_1.1.2 ann
cd /home/slongle/L1-Skeleton/PointCloud/depends/ANN/ann
sudo make linux-g++

cd /home/slongle/L1-Skeleton/PointCloud/depends/VCG
sudo wget https://github.com/jasonkena/L1-Skeleton/files/10715278/vcglib-1.0.0.zip
sudo unzip vcglib-1.0.0.zip
sudo mv vcglib-1.0.0 vcg
cd /home/slongle/L1-Skeleton/PointCloud/depends/VCG/vcg
# sudo cmake . && make

cd /home/slongle/L1-Skeleton/PointCloud
mkdir build
cd build
cmake ..
make

ENTRYPOINT ["./PointCloudL1"]
