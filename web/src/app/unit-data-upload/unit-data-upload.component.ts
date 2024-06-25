import { AfterViewInit, Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { FileTransferService, ConnectTestService, QueryNeo4jService } from '../app-services';
import { CpaStructur, ExperimentStructur, OtherStructur, defaultCpaData, defaultExperiment, defaultPrePostData, defaultProcess } from '../app-config';

@Component({
  selector: 'app-unit-data-upload',
  templateUrl: './unit-data-upload.component.html',
  styleUrls: ['./unit-data-upload.component.css']
})
export class UnitDataUploadComponent implements OnInit, AfterViewInit, OnChanges {
  @ViewChild('fileInput1') fileInput1!: ElementRef;
  @ViewChild('fileInput2') fileInput2!: ElementRef;

  uploadedFiles: { file_name: string, result: string, neo4j: string }[] = [];
  @Input() onlyDir!: boolean;
  @Input() allowMultiple!: boolean;
  @Input() allowFolder!: boolean;
  @Input() data_type!: 'PreData' | 'PostData' | 'CPA' | 'Experiment' | 'Process';

  dataStoreStatus: 'error' | 'success' | 'pending' = 'pending'

  selectedFiles: { [key: string]: string } = {}

  defaultData!: CpaStructur | OtherStructur | ExperimentStructur

  constructor(
    private fileTransferService: FileTransferService,
    // private connectTestService: ConnectTestService,
    private queryNeo4jService: QueryNeo4jService
  ) {

  }
  ngOnChanges(changes: SimpleChanges): void {
    if (!changes['data_type'].isFirstChange()) {
      this.ngOnInit()
      this.ngAfterViewInit()
    }
  }

  clearFileInput() {
    if (this.fileInput1 && this.fileInput1.nativeElement) {
      this.fileInput1.nativeElement.value = '';
    }
    if (this.fileInput2 && this.fileInput2.nativeElement) {
      this.fileInput2.nativeElement.value = '';
    }
  }

  ngOnInit() {
    if (this.data_type == 'CPA') {
      this.defaultData = defaultCpaData
    } else if (this.data_type == 'Experiment') {
      this.defaultData = defaultExperiment
    } else if (this.data_type == 'PreData') {
      this.defaultData = defaultPrePostData
    } else if (this.data_type == 'PostData') {
      this.defaultData = defaultPrePostData
    } else if (this.data_type == 'Process') {
      this.defaultData = defaultProcess
    }
  }

  ngAfterViewInit() {
    // this.connectTestService.cleanDataStoreFile(this.data_type).then((rep) => {
    //   this.dataStoreStatus = rep
    //   this.uploadedFiles = []
    //   this.selectedFiles = {};
    //   this.clearFileInput()
    // })
    this.uploadedFiles = []
    this.selectedFiles = {};
    this.clearFileInput()
  }

  onFileSelected(event: any) {
    const files: FileList = event.target.files;
    if (files.length > 0) {
      if (this.data_type == 'Experiment') {
        this.fileTransferService.fileUpload(files, this.data_type + 'Upload').then((res) => {
          this.uploadedFiles = [...this.uploadedFiles, ...(JSON.parse(res.replace(/'/g, '"')))]
          this.uploadedFiles.forEach(file => {
            this.selectedFiles[file.file_name] = file.neo4j
          });
        })
      }
      else {
        this.fileTransferService.fileUpload(files, this.data_type).then((res) => {
          this.uploadedFiles = [...this.uploadedFiles, ...(JSON.parse(res.replace(/'/g, '"')))]
          this.uploadedFiles.forEach(file => {
            this.selectedFiles[file.file_name] = file.neo4j
          });
        })
      }
    }
  }

  selectedOrNot(file: { file_name: string, result: string, neo4j: string }) {
    if (file.neo4j == 'undo') {
      return false
    }
    else {
      return true
    }
  }

  disabledOrNot(file: { file_name: string, result: string, neo4j: string }) {
    if (file.result != 'success') {
      return true
    }
    else {
      return false
    }
  }

  onSelected(event: any) {
    if (event['options'][0]['_selected']) {
      if (this.selectedFiles[event['options'][0]['_value']] == 'undo') {
        this.selectedFiles[event['options'][0]['_value']] = 'waiting'
      }
    } else {
      if (this.selectedFiles[event['options'][0]['_value']] == 'waiting') {
        this.selectedFiles[event['options'][0]['_value']] = 'undo'
      }
    }
  }

  feedToDB() {
    if (this.data_type == 'Experiment') {
      let error_store: Promise<string>[] = []
      for (let i = 0; i < (Object.keys(this.selectedFiles).length - 1); i++) {
        error_store.push(new Promise<string>(async (resolve, reject) => {
          var file_name = Object.keys(this.selectedFiles)[i]
          if (this.selectedFiles[file_name] == 'waiting') {
            this.selectedFiles[file_name] = 'doing'
            var self = this;
            (function (fileName: string) {
              self.queryNeo4jService.feedNeo4j(self.data_type + 'Upload', fileName).then((res: any) => {
                resolve(res)
                self.selectedFiles[fileName] = res;
              }).finally(() => {
                self.selectedFiles = { ...self.selectedFiles };
              });
            }).call(this, file_name);
          }
        }))

      }

      Promise.all(error_store)
        .then((results) => {
          const allResolved = results.every((result) => result !== 'error');

          if (allResolved) {
            var file_name = Object.keys(this.selectedFiles)[Object.keys(this.selectedFiles).length-1]
            if (this.selectedFiles[file_name] == 'waiting') {
              this.selectedFiles[file_name] = 'doing'
              var self = this;
              (function (fileName: string) {
                self.queryNeo4jService.feedNeo4j(self.data_type + 'Upload', fileName).then((res: any) => {
                  self.selectedFiles[fileName] = res;
                }).finally(() => {
                  self.selectedFiles = { ...self.selectedFiles };
                });
              }).call(this, file_name);
            }
          } else {
            this.selectedFiles[Object.keys(this.selectedFiles)[Object.keys(this.selectedFiles).length]] = 'error'
          }
        }).catch((error) => {
          this.selectedFiles[Object.keys(this.selectedFiles)[Object.keys(this.selectedFiles).length]] = 'error'
        });

    }
    else {
      for (var file_name in this.selectedFiles) {
        if (this.selectedFiles[file_name] == 'waiting') {
          this.selectedFiles[file_name] = 'doing'
          var self = this;
          (function (fileName: string) {
            self.queryNeo4jService.feedNeo4j(self.data_type, fileName).then((res: any) => {
              self.selectedFiles[fileName] = res;
            }).finally(() => {
              self.selectedFiles = { ...self.selectedFiles };
            });
          }).call(this, file_name);
        }
      }
    }
  }
  deleteAll() {
    if (confirm(`All about ${this.data_type} that not saved in the database will be lost! Are you sure to continue?`)) {
      this.ngAfterViewInit()
    }
  }
}
