import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.*
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            var text by remember { mutableStateOf("Noch nichts geladen") }

            Button(
                onClick = {
                    Thread {
                        try {
                            val inhalt = URL(
                                "https://example.com/notiz.txt"
                            ).readText()

                            runOnUiThread {
                                text = inhalt
                            }
                        } catch (e: Exception) {
                            runOnUiThread {
                                text = "Fehler: ${e.message}"
                            }
                        }
                    }.start()
                }
            ) {
                Text("Datei herunterladen")
            }

            Text(text)
        }
    }
}
