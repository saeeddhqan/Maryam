export class MaryamModule {
constructor(
  public modulename: string,
  public moduleargs: string[],
){}
}

export class MaryamOptions{
  constructor(
    public agent: string,
    public api_mode: string,
    public protocol: string,
    public proxy: string,
    public rand_agent: boolean,
    public timeout: number,
    public update_check: boolean,
    public verbosity: number   
  ) {}
}
