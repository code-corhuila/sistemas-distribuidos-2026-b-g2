package co.edu.corhuila.property.payment.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.time.Instant;
import java.util.Base64;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;

// Story: [security] A Pago is read only by its owner (STRIDE E).
@SpringBootTest
@AutoConfigureMockMvc
class PagoAuthorizationNegativeTest {

    private static final KeyPair SERVICE_KEY = newKey();

    @DynamicPropertySource
    static void publicKey(DynamicPropertyRegistry registry) {
        String pem = "-----BEGIN PUBLIC KEY-----\n"
                + Base64.getMimeEncoder(64, "\n".getBytes()).encodeToString(SERVICE_KEY.getPublic().getEncoded())
                + "\n-----END PUBLIC KEY-----\n";
        registry.add("JWT_PUBLIC_KEY", () -> pem);
    }

    @Autowired
    private MockMvc mvc;

    @Test
    void withoutTokenAnswers401() throws Exception {
        mvc.perform(get("/api/v1/pagos/3f2b7c1e-0000-4000-8000-000000000001"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.error").value("UNAUTHORIZED"));
    }

    @Test
    void unsignedTokenWithAlgNoneAnswers401() throws Exception {
        Base64.Encoder url = Base64.getUrlEncoder().withoutPadding();
        String unsigned = url.encodeToString("{\"alg\":\"none\"}".getBytes(StandardCharsets.UTF_8)) + "."
                + url.encodeToString(("{\"sub\":\"00000000-0000-4000-8000-000000000002\",\"roles\":[\"ADMIN\"],\"exp\":"
                        + Instant.now().plusSeconds(600).getEpochSecond() + "}").getBytes(StandardCharsets.UTF_8)) + ".";
        mvc.perform(get("/api/v1/pagos/3f2b7c1e-0000-4000-8000-000000000001").header("Authorization", "Bearer " + unsigned))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.error").value("UNAUTHORIZED"));
    }

    private static KeyPair newKey() {
        try {
            KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
            generator.initialize(2048);
            return generator.generateKeyPair();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }
}
