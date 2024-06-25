import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { backendUrl, dataStoreName } from '../app-config';

@Injectable({
  providedIn: 'root'
})
export class CalculatorService {
  constructor(
    private http: HttpClient,
  ) { }

  getMeanAndVariance(dataList: string[]): Promise<any> {
    const headers = { 'content-type': 'application/json' }
    const body = JSON.stringify({
      'data': dataList
    });
    var promise = new Promise<any>((resolve, reject) => {
      this.http.post(`${backendUrl}/getMeanAndVariance/`, body, { 'headers': headers })
        .subscribe((rep: any) => {
          resolve(rep)
        })
    })
    return promise
  }

  anovaTest(data: { [key: string]: [string, string][] }): Promise<any> {
    const headers = { 'content-type': 'application/json' }
    const body = JSON.stringify(data);
    var promise = new Promise<any>((resolve, reject) => {
      this.http.post(`${backendUrl}/anovaTest/`, body, { 'headers': headers })
        .subscribe((rep: any) => {
          resolve(rep)
        })
    })
    return promise
  }

  buildColumn(data: { [key: string]: [string, string][] }): Promise<string> {
    const headers = { 'content-type': 'application/json' }
    const body = JSON.stringify(data);
    var promise = new Promise<string>((resolve, reject) => {
      this.http.post(`${backendUrl}/buildColumn/`, body, { 'headers': headers })
        .subscribe((rep: any) => {
          resolve(rep)
        })
    })
    return promise
  }
}
