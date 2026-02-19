/** Tests for frontend project initialization - Story 1.1 */
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Frontend Project Initialization', () => {
  const frontendRoot = path.join(process.cwd(), 'frontend');
  
  it('should have Next.js package.json', () => {
    const pkgPath = path.join(frontendRoot, 'package.json');
    expect(fs.existsSync(pkgPath)).toBe(true);
    
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    expect(pkg.dependencies.next).toBeDefined();
    expect(pkg.dependencies.react).toBeDefined();
  });

  it('should have TypeScript configured', () => {
    const tsconfigPath = path.join(frontendRoot, 'tsconfig.json');
    expect(fs.existsSync(tsconfigPath)).toBe(true);
    
    const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf-8'));
    expect(tsconfig.compilerOptions.strict).toBe(true);
    expect(tsconfig.compilerOptions.paths['@/*']).toEqual(['./src/*']);
  });

  it('should have Tailwind CSS configured', () => {
    const tailwindPath = path.join(frontendRoot, 'postcss.config.mjs');
    expect(fs.existsSync(tailwindPath)).toBe(true);
  });

  it('should have environment files', () => {
    expect(fs.existsSync(path.join(frontendRoot, '.env.local'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, '.env.example'))).toBe(true);
  });

  it('should have feature-based directory structure', () => {
    expect(fs.existsSync(path.join(frontendRoot, 'src/features'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/shared'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/app'))).toBe(true);
  });

  it('should have required features directories', () => {
    expect(fs.existsSync(path.join(frontendRoot, 'src/features/auth'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/features/lists'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/features/items'))).toBe(true);
  });

  it('should have shared directories', () => {
    expect(fs.existsSync(path.join(frontendRoot, 'src/shared/components'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/shared/lib'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/shared/hooks'))).toBe(true);
    expect(fs.existsSync(path.join(frontendRoot, 'src/shared/stores'))).toBe(true);
  });

  it('should have NEXT_PUBLIC_API_URL in .env.local', () => {
    const envPath = path.join(frontendRoot, '.env.local');
    const envContent = fs.readFileSync(envPath, 'utf-8');
    expect(envContent).toContain('NEXT_PUBLIC_API_URL');
  });
});
