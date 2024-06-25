import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { backendUrl, dataStoreName } from '../app-config';

@Injectable({
  providedIn: 'root'
})

export class FileTransferService {

  constructor(
    private http: HttpClient,
  ) { }

  fileUpload(selectedFile: FileList, data_type: string): Promise<any> {
    var promise = new Promise<any>((resolve, reject) => {
      const formData = new FormData();
      for (let i = 0; i < selectedFile.length; i++) {
        if (data_type == 'CPA' || data_type == 'ExperimentUpload') {
          formData.append('files', selectedFile[i], selectedFile[i].webkitRelativePath);
        } else {
          formData.append('files', selectedFile[i], selectedFile[i].name);
        }

      }
      this.http.post(`${backendUrl}/fileUpload/?data_type=${data_type}&data_store=${dataStoreName}`, formData)
        .subscribe((rep: any) => {
          resolve(rep)
        })

    })
    return promise
  }

  fileCreate(file_name:string, data_type: 'PreData' | 'PostData' | 'CPA' | 'Experiment' | 'Process', data: {}):Promise<any> {
    var promise = new Promise<any>((resolve, reject) => {
      const formData = new FormData();
      formData.append('files', new Blob([JSON.stringify(data)], { type: 'application/json' }), file_name);
      
      this.http.post(`${backendUrl}/fileCreate/?data_type=${data_type}&data_store=${dataStoreName}`, formData)
        .subscribe((rep: any) => {
          resolve(rep)
        })

    })
    return promise
  }
}
