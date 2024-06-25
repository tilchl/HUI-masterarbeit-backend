import { Component } from '@angular/core';
import { QueryNeo4jService } from '../app-services';

@Component({
  selector: 'app-unit-database-check',
  templateUrl: './unit-database-check.component.html',
  styleUrls: ['./unit-database-check.component.css']
})
export class UnitDatabaseCheckComponent {
  checkItems: { [key: string]: 'pending' | 'success' | 'error' | JSON } =
    {
      'cryoConnection': 'pending',
      'cpaConnection': 'pending',
      'cryoData': 'pending',
      'cpaData': 'pending',
    }
  connectionStatus: string = 'pending'
  panelOpenState = false

  constructor(
    private queryNeo4jService: QueryNeo4jService
  ) {
    this.queryNeo4jService.queryTest('cryo').then((rep) => {
      if (rep != 'error') {
        this.checkItems['cryoConnection'] = 'success'
        this.checkItems['cryoData'] = JSON.parse(rep.replace(/'/g, '"'))
      } else {
        this.checkItems['cryoConnection'] = 'error'
        this.checkItems['cryoData'] = 'error'
      }
      this.updateStatus()
    })
    this.queryNeo4jService.queryTest('cpa').then((rep) => {
      if (rep != 'error') {
        this.checkItems['cpaConnection'] = 'success'
        this.checkItems['cpaData'] = JSON.parse(rep.replace(/'/g, '"'))
      } else {
        this.checkItems['cpaConnection'] = 'error'
        this.checkItems['cpaData'] = 'error'
      }
      this.updateStatus()
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
