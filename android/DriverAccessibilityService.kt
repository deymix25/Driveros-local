package com.driveros.local

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo

class DriverAccessibilityService : AccessibilityService() {

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        val rootNode = rootInActiveWindow ?: return
        val packageName = event?.packageName?.toString() ?: ""

        val allowedApps = listOf("com.ubercab.driver", "com.didi.echo.seller", "com.cabify.driver")
        if (!allowedApps.contains(packageName)) {
            rootNode.recycle()
            return
        }

        val extractedTexts = mutableListOf<String>()
        traverseNodeTree(rootNode, extractedTexts)
        rootNode.recycle()

        if (extractedTexts.isNotEmpty()) {
            val intent = Intent("com.driveros.OFFER_DETECTED").apply {
                putExtra("PACKAGE_NAME", packageName)
                putStringArrayListExtra("TEXT_NODES", ArrayList(extractedTexts))
            }
            sendBroadcast(intent)
        }
    }

    private fun traverseNodeTree(node: AccessibilityNodeInfo?, resultList: MutableList<String>) {
        if (node == null) return
        if (!node.text.isNullOrEmpty()) {
            resultList.add(node.text.toString().trim())
        }
        for (i in 0 until node.childCount) {
            val child = node.getChild(i)
            traverseNodeTree(child, resultList)
            child?.recycle()
        }
    }

    override fun onInterrupt() {}
}
