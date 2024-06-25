import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SeiteAboutUsComponent } from '../seite-about-us/seite-about-us.component';
import { SeiteWelcomeComponent } from '../seite-welcome/seite-welcome.component';
import { SeiteAboutThisComponent } from '../seite-about-this/seite-about-this.component';
import { SeiteTechnologyComponent } from '../seite-technology/seite-technology.component';
import { SeiteDatabaseComponent } from '../seite-database/seite-database.component';
import { SeiteNnComponent } from '../seite-nn/seite-nn.component';
import { SeiteStartComponent } from '../seite-start/seite-start.component';
import { SeiteDataStorageComponent } from '../seite-data-storage/seite-data-storage.component';
import { SeiteDataAnalyseComponent } from '../seite-data-analyse/seite-data-analyse.component';


const routes: Routes = [
  { path: '', component: SeiteWelcomeComponent },
  { path: 'about-us', component: SeiteAboutUsComponent },
  { path: 'about-this', component: SeiteAboutThisComponent },
  { path: 'technology', component: SeiteTechnologyComponent },
  { path: 'database', component: SeiteDatabaseComponent },
  { path: 'nn', component: SeiteNnComponent },
  { path: 'start', component: SeiteStartComponent, children: [
    { path: '', redirectTo: 'guide', pathMatch: 'full' }, // Redirect /nn to /nn/guide
    { path: 'guide', component: SeiteDataAnalyseComponent },
    { path: 'data-storage', component: SeiteDataStorageComponent },
    { path: 'data-analyse', component: SeiteDataAnalyseComponent },
    { path: 'cells-count', component: SeiteDataAnalyseComponent },
    { path: 'survivalrate-predict', component: SeiteDataAnalyseComponent },
    { path: 'parameter-optimize', component: SeiteDataAnalyseComponent },
  ]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
