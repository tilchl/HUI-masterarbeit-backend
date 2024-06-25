import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteDataStorageComponent } from './seite-data-storage.component';

describe('SeiteDataStorageComponent', () => {
  let component: SeiteDataStorageComponent;
  let fixture: ComponentFixture<SeiteDataStorageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteDataStorageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteDataStorageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
