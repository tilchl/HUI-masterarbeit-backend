import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitEditDatabaseComponent } from './unit-edit-database.component';

describe('UnitEditDatabaseComponent', () => {
  let component: UnitEditDatabaseComponent;
  let fixture: ComponentFixture<UnitEditDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitEditDatabaseComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitEditDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
