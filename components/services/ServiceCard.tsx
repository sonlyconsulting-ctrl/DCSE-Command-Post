import type { ServiceProduct } from '../../types/services';

export interface ServiceCardProps {
  service: ServiceProduct;
  className?: string;
}

/** Presentational contract: the caller supplies all service data. */
export default function ServiceCard({ service, className }: ServiceCardProps) {
  return (
    <article className={className}>
      <p>{service.parent_brand}</p>
      <h2>{service.name}</h2>
      <p>{service.hero}</p>
      <p>{service.description}</p>
      <ul>
        {service.capabilities.map((capability) => (
          <li key={capability.title}>{capability.title}</li>
        ))}
      </ul>
    </article>
  );
}
