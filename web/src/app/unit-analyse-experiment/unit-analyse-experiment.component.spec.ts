import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseExperimentComponent } from './unit-analyse-experiment.component';

describe('UnitAnalyseExperimentComponent', () => {
  let component: UnitAnalyseExperimentComponent;
  let fixture: ComponentFixture<UnitAnalyseExperimentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseExperimentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
