import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiRequestService {
  readonly api_url: string = "http://localhost:8000/formInput/"
  command_str: string


  constructor(private http_client:HttpClient) { }

  runCmd(command: { [meta: string]: string }): Observable<any[]> {
    this.command_str = "?modulename=" + command["modulename"] + "&command=" + command["command"]
    return this.http_client.get<any[]>(this.api_url + this.command_str)
  }
}
