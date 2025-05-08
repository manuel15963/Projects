package pe.edu.vallegrande.project.model;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Data
@Table(name = "Products")
public class Products {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "productos_seq")
    @SequenceGenerator(name = "productos_seq", sequenceName = "Productos_seq", allocationSize = 1)
    @Column(name = "product_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "category_id")
    private Categories category;

    @Column(name = "name")
    private String name;

    @Column(name = "description")
    private String description;

    @Column(name = "unit_price")
    private BigDecimal unitPrice;

    @Column(name = "stocks")
    private Integer stocks;

    @Column(name = "expiration_date")
    private LocalDate expirationDate;

    @Column(name = "Status")
    private String status; // Puede ser '1' o '0'
}
