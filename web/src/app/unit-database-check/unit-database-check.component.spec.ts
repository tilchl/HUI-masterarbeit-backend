import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitDatabaseCheckComponent } from './unit-database-check.component';

describe('UnitDatabaseCheckComponent', () => {
  let component: UnitDatabaseCheckComponent;
  let fixture: ComponentFixture<UnitDatabaseCheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitDatabaseCheckComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitDatabaseCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
