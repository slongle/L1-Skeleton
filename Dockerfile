# ubuntu lts
FROM ubuntu:20.04

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install -y software-properties-common build-essential cmake git wget unzip
# RUN apt install -y python3 python3-pip

# install Qt4
RUN apt-add-repository -y ppa:rock-core/qt4
RUN apt install -y qt4-default

RUN apt install -y libglew-dev freeglut3-dev libeigen3-dev libann-dev

# clone repo in /home
RUN git clone https://github.com/jasonkena/L1-Skeleton.git /home/L1-Skeleton
WORKDIR /home/L1-Skeleton
RUN git submodule update --init --recursive
RUN git reset --hard e0452579b7945ccd8407e70eb11703e4b3eca612

WORKDIR /home/L1-Skeleton/PointCloud/depends/ANN
RUN wget https://github.com/jasonkena/L1-Skeleton/files/10715019/ann_1.1.2.zip
RUN unzip ann_1.1.2.zip
RUN mv ann_1.1.2 ann
WORKDIR /home/L1-Skeleton/PointCloud/depends/ANN/ann
RUN make linux-g++

WORKDIR /home/L1-Skeleton/PointCloud/depends/VCG
RUN wget https://github.com/jasonkena/L1-Skeleton/files/10715278/vcglib-1.0.0.zip
RUN unzip vcglib-1.0.0.zip
RUN mv vcglib-1.0.0 vcg
WORKDIR /home/L1-Skeleton/PointCloud/depends/VCG/vcg
# RUN cmake . && make

WORKDIR /home/L1-Skeleton/PointCloud
RUN cmake . && make

ENTRYPOINT ["./PointCloudL1"]
