import { TestBed } from '@angular/core/testing';

import { ApiRequestService } from './api-request.service';

describe('ApiRequestService', () => {
  let service: ApiRequestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApiRequestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
