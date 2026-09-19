export interface CapacitorConfig {
  appId: string;
  appName: string;
  webDir: string;
  bundledWebRuntime?: boolean;
  server?: {
    androidScheme?: string;
    cleartext?: boolean;
    url?: string;
  };
}

const config: CapacitorConfig = {
  appId: 'com.sentinela.app',
  appName: 'Sentinel-A',
  webDir: 'out',
  server: {
    androidScheme: 'https',
    cleartext: true,
  },
};

export default config;
