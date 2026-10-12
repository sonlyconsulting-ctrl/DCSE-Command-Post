import type { ServiceBrand, ServiceProduct } from '../../types/services';

export interface HeroProps {
  brand: ServiceBrand;
  heading: ServiceProduct['hero'];
  description: ServiceProduct['description'];
  primaryHref: string;
  secondaryHref?: string;
  className?: string;
}

/** Presentational contract: content and navigation are supplied by the caller. */
export default function Hero({
  brand,
  heading,
  description,
  primaryHref,
  secondaryHref,
  className,
}: HeroProps) {
  return (
    <section className={className}>
      <p>{brand.name}</p>
      <p>{brand.tagline}</p>
      <h1>{heading}</h1>
      <p>{description}</p>
      <nav aria-label="Primary actions">
        <a href={primaryHref}>{brand.cta_primary}</a>
        {secondaryHref !== undefined && (
          <a href={secondaryHref}>{brand.cta_secondary}</a>
        )}
      </nav>
    </section>
  );
}
