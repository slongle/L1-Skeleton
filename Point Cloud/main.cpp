#include "Algorithm/Skeletonization.h"
#include "Console.h"
#include "DataMgr.h"
#include "ParameterMgr.h"
#include "mainwindow.h"
#include <QString>

int main(int argc, char *argv[]) {
  CConsoleOutput::Instance();

  if (argc == 1) {
    glutInit(&argc, argv);
    CConsoleOutput::Instance();
    // QApplication app(argc, argv);
    QApplication::setStyle(QStyleFactory::create("cleanlooks"));
    /*
    "windows", "motif", "cde", "plastique" and "cleanlooks". Depending on the
    platform, "windowsxp", "windowsvista" and "macintosh" may be available. Note
    that keys are case insensitive.
    */

    QApplication a(argc, argv);
    MainWindow *mainWindow = new MainWindow(NULL);
    mainWindow->showMaximized();
    // mainWindow->show();

    return a.exec();
  } else {
    if (argc != 4) {
      cout << "Usage: " << argv[0] << " input.ply output.skel config.json" << endl;
    } else {
      global_paraMgr.loadSkeletonConfigJson(argv[3]);
      DataMgr *dataMgr = new DataMgr(global_paraMgr.getDataParameterSet());
      dataMgr->loadPlyToOriginal(argv[1]);
      dataMgr->downSamplesByNum(true); // do nondeterministic downsampling
      // dataMgr->downSamplesByNum(false); // do deterministic downsampling
      Skeletonization *skeletonization =
          new Skeletonization(global_paraMgr.getSkeletonParameterSet());
      skeletonization->setFirstIterate();
      skeletonization->setInput(dataMgr);

      double current_radius = global_paraMgr.skeleton.getDouble("CGrid Radius");
      global_paraMgr.skeleton.setValue("Initial Radius",
                                       DoubleValue(current_radius));

      int num_iter = global_paraMgr.skeleton.getInt("Max Num Iterations");

      for (int i = 0; i < num_iter; i++) {
        global_paraMgr.skeleton.setValue("Run Auto Wlop One Step",
                                         BoolValue(true));
        // adapted from runPointCloudAlgorithm
        skeletonization->setInput(dataMgr);
        skeletonization->run();
        skeletonization->clear();
        global_paraMgr.skeleton.setValue("Run Auto Wlop One Step",
                                         BoolValue(true));

        if (global_paraMgr.skeleton.getBool(
                "The Skeletonlization Process Should Stop")) {
          break;
        }
      }

      dataMgr->saveSkeletonAsSkel(argv[2]);
      cout << "Skeleton saved to " << argv[2] << endl;
    }
  }
}
