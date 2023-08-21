#include "Algorithm/Skeletonization.h"
#include "Console.h"
#include "DataMgr.h"
#include "ParameterMgr.h"
#include "mainwindow.h"
#include <QString>

class FakeGUI {
  public:
    DataMgr dataMgr;

    WLOP wlop;
    NormalSmoother norSmoother;
    Skeletonization skeletonization;
    Upsampler upsampler;
    RichParameterSet *para;

  public:
    FakeGUI()
        : para(global_paraMgr.getGlareaParameterSet()), dataMgr(global_paraMgr.getDataParameterSet()),
          wlop(global_paraMgr.getWLopParameterSet()), norSmoother(global_paraMgr.getNormalSmootherParameterSet()),
          skeletonization(global_paraMgr.getSkeletonParameterSet()),
          upsampler(global_paraMgr.getUpsamplingParameterSet()) {}

    void ClearPointCloud() { dataMgr.clearData(); }
    void ImportPointCloud(const QString &filename) {
        dataMgr.loadPlyToSample(filename);
        dataMgr.getInitRadiuse();
        dataMgr.recomputeQuad();
        dataMgr.recomputeBox();
        wlop.setFirstIterate();
        skeletonization.setFirstIterate();
    }
    void SaveSkeleton(const QString &filename) {
        dataMgr.saveSkeletonAsSkel(filename);
    }

    void InitialSampling(const int &sampleNum) {
        dataMgr.para->setValue("Down Sample Num", DoubleValue(sampleNum));
        dataMgr.downSamplesByNum();
        dataMgr.skeleton.clear();
    }
    void ExtractSkeleton() {
        int num_iter = global_paraMgr.skeleton.getInt("Max Num Iterations");

        for (int i = 0; i < num_iter; i++) {
            global_paraMgr.skeleton.setValue("Run Auto Wlop One Step", BoolValue(true));
            // adapted from runPointCloudAlgorithm
            skeletonization.setInput(&dataMgr);
            skeletonization.run();
            skeletonization.clear();
            global_paraMgr.skeleton.setValue("Run Auto Wlop One Step", BoolValue(true));

            if (global_paraMgr.skeleton.getBool("The Skeletonlization Process Should Stop")) {
                break;
            }
        }
    }

    void Process(const QString& pointCloudFilename, const QString& skeletonFilename, const int& sampleNum) {
        ClearPointCloud();
        ImportPointCloud(pointCloudFilename);
        InitialSampling(sampleNum);        

        ExtractSkeleton();
        SaveSkeleton(skeletonFilename);
    }
};

int main(int argc, char* argv[]) {
    FakeGUI fakeGUI;
    QString pointCloudFilename(argv[1]);
    QString skeletonFilename(argv[2]);
    int sampleNum = std::atoi(argv[3]);
    fakeGUI.Process(pointCloudFilename, skeletonFilename, sampleNum);
}