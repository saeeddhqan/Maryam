import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormsDisplayComponent } from './forms-display.component';

describe('FormsDisplayComponent', () => {
  let component: FormsDisplayComponent;
  let fixture: ComponentFixture<FormsDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormsDisplayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormsDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
