export interface product {
    id?: number;
    name: string;
    description: string;
    unitPrice: number;
    stocks: number;
    expirationDate: string;
    status: string;
    category: {
      id?: number;
      name?: string;
    };
  }
  