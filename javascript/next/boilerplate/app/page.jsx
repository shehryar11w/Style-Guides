import Link from 'next/link';
import Button from '@/components/ui/Button/Button';

export default function HomePage() {
  return (
    <div className="home">
      <h1>Welcome to Next.js App</h1>
      <p>This is a boilerplate Next.js application following best practices.</p>
      <Button>
        <Link href="/about">Get Started</Link>
      </Button>
    </div>
  );
}

