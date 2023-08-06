// import _ from 'underscore';
import daikon from 'daikon';

import FileModel from '@girder/core/models/FileModel';
import { restRequest } from '@girder/core/rest';
import { wrap } from '@girder/core/utilities/PluginUtils';

import DicomItemView from '@girder/dicom-viewer/views/DicomView';

const DicomFileModel = FileModel.extend({
    getSlice: function () {
        if (!this._slice) {
            // Cache the slice on the model
            this._slice = restRequest({
                url: this.get('archivePath') ? `file/${this.get('archiveId')}/archive/download` : `file/${this.id}/download`,
                data: this.get('archivePath') ? { path: this.get('archivePath') } : {},
                xhrFields: {
                    responseType: 'arraybuffer'
                }
            })
                .then((resp) => {
                    const dataView = new DataView(resp);
                    return daikon.Series.parseImage(dataView);
                });
        }
        return this._slice;
    }
});

wrap(DicomItemView, 'initialize', function (initialize, settings) {
    const result = initialize.call(this, settings);
    if (settings.item.get('dicom').files[0].archivePath) {
        var files = settings.item.get('dicom').files;
        files.forEach(function (file, idx) {
            file.archiveId = file._id;
            file._id = idx;
        });
        const WrappedFileCollection = this._files.constructor.extend({
            model: DicomFileModel
        });
        this._files = new WrappedFileCollection(files);
        this.listenTo(this._files, 'g:selected', this._onSelectionChanged);
    }
    return result;
});
