import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseSelectMenuComponent } from './unit-analyse-select-menu.component';

describe('UnitAnalyseSelectMenuComponent', () => {
  let component: UnitAnalyseSelectMenuComponent;
  let fixture: ComponentFixture<UnitAnalyseSelectMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseSelectMenuComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseSelectMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
