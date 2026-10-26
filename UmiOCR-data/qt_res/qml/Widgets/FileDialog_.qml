// =========================================
// =============== 文件选择窗 ===============
// =========================================

import QtQuick 2.15
import Qt.labs.platform 1.1

FileDialog {
    id: dlg
    property var fileUrls_: [] // 缓存处理好的 fileUrls
    property alias fileUrls: dlg.files
    property bool selectMultiple: false
    property bool selectExisting: true
    property bool selectFolder: false

    fileMode: selectMultiple ? FileDialog.OpenFiles : FileDialog.OpenFile

    onAccepted: {
        fileUrls_ = qmlapp.utilsConnector.QUrl2String(files)
    }
}