package com.example.notizenapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            NotizenApp()
        }
    }
}

@Composable
fun NotizenApp() {
    var text by remember { mutableStateOf("") }
    val notizen = remember { mutableStateListOf<String>() }

    MaterialTheme {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                label = { Text("Neue Notiz") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(8.dp))

            Button(
                onClick = {
                    if (text.isNotBlank()) {
                        notizen.add(text)
                        text = ""
                    }
                }
            ) {
                Text("Speichern")
            }

            Spacer(modifier = Modifier.height(16.dp))

            LazyColumn {
                items(notizen) { notiz ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                    ) {
                        Text(
                            text = notiz,
                            modifier = Modifier.padding(16.dp)
                        )
                    }
                }
            }
        }
    }
}
