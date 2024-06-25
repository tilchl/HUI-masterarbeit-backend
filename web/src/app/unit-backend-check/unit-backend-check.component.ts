import { Component } from '@angular/core';
import { ConnectTestService } from '../app-services';
import { dataStoreName } from '../app-config';

@Component({
  selector: 'app-unit-backend-check',
  templateUrl: './unit-backend-check.component.html',
  styleUrls: ['./unit-backend-check.component.css']
})
export class UnitBackendCheckComponent {
  checkItems: { [key: string]: 'pending' | 'success' | 'error' | 'exists' } =
    {
      'backendConnection': 'pending',
      'dataStoreExistence': 'pending',
      'dataStoreIntegrityCpa': 'pending',
      'dataStoreIntegrityExp': 'pending',
      'dataStoreIntegrityPredata': 'pending',
      'dataStoreIntegrityPostdata': 'pending',
      'dataStoreIntegrityProcess': 'pending'
    }
  connectionStatus: string = 'pending'
  panelOpenState = false
  dataStoreName = dataStoreName

  constructor(
    private connectTestService: ConnectTestService,
  ) {
    this.connectTestService.testBackend().then((rep) => {
      this.checkItems['backendConnection'] = rep
      this.updateStatus()
    })
    this.connectTestService.cleanDataStore().then((rep) => {
      this.checkItems['dataStoreExistence'] = rep
      this.updateStatus()
      this.connectTestService.testDataStoreFile(["CPA","Experiment","PreData","PostData","Process"]).then((rep) => {
        this.checkItems['dataStoreIntegrityCpa'] = rep['CPA']
        this.checkItems['dataStoreIntegrityExp'] = rep['Experiment']
        this.checkItems['dataStoreIntegrityPredata'] = rep['PreData']
        this.checkItems['dataStoreIntegrityPostdata'] = rep['PostData']
        this.checkItems['dataStoreIntegrityProcess'] = rep['Process']
        this.updateStatus()
      })
    })
  }
  updateStatus() {
    const values = Object.values(this.checkItems);

    if (values.includes('pending')) {
      this.connectionStatus = 'pending';
    } else if (values.includes('error')) {
      this.connectionStatus = 'error';
    } else {
      this.connectionStatus = 'success';
    }
  }
}
