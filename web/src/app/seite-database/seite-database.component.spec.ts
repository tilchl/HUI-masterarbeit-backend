import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteDatabaseComponent } from './seite-database.component';

describe('SeiteDatabaseComponent', () => {
  let component: SeiteDatabaseComponent;
  let fixture: ComponentFixture<SeiteDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteDatabaseComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
