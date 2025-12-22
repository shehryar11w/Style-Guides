'use client';

export default function Error({ error, reset }) {
  return (
    <div className="error">
      <h2>Something went wrong!</h2>
      <p>{error?.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}

