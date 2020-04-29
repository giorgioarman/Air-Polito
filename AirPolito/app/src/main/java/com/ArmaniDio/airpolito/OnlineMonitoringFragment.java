package com.ArmaniDio.airpolito;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.net.http.SslError;
import android.os.Bundle;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.SslErrorHandler;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;


public class OnlineMonitoringFragment extends Fragment {

    private final static String TAG = "OnlineMonitoringFrag";
    private static String AIRPOLITOURL = "https://www.airpolito.it/online-monitoraggio-android/";

    private WebView wvOM;
    private ProgressBar pbLoading;

    private int waitingCount = 0;

    public OnlineMonitoringFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_online_monitoring, container, false);
        wvOM = view.findViewById(R.id.wvOnLineMonitoring);
        pbLoading = view.findViewById(R.id.pb_loading);

        setWebView();

        // Inflate the layout for this fragment
        return view;
    }

    private void setWebView() {
        setFragmentLoading(true);

        WebSettings webSettings = wvOM.getSettings();
        webSettings.setLoadsImagesAutomatically(true);
        webSettings.setJavaScriptEnabled(true);
        wvOM.setWebChromeClient(new WebChromeClient());

        wvOM.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                Log.i(TAG, "loading: build.VERSION_CODES.N");
                view.loadUrl(url);
                return true;
            }

            @Override
            public void onPageStarted(
                    WebView view, String url, Bitmap favicon) {
                Log.i(TAG, "page started:"+url);
                super.onPageStarted(view, url, favicon);
            }
            @Override
            public void onPageFinished(WebView view, final String url) {
                Log.i(TAG, "page finished:"+url);
                setFragmentLoading(false);
            }
            @Override
            public void onReceivedSslError(WebView view, final SslErrorHandler handler, SslError er) {
                final AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
                builder.setMessage(R.string.notification_error_ssl_cert_invalid);
                builder.setPositiveButton("continue", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        handler.proceed();
                    }
                });
                builder.setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        handler.cancel();
                    }
                });
                final AlertDialog dialog = builder.create();
                dialog.show();

            }
        });

        wvOM.loadUrl(AIRPOLITOURL);
    }

    private synchronized void setFragmentLoading(boolean loading) {
        // this method is necessary to show the user when the activity is doing a network operation
        // as downloading data or uploading data
        // how to use: call with loading = true to notify that a new transmission has been started
        // call with loading = false to notify end of transmission

        if (loading) {
            if (waitingCount == 0)
                pbLoading.setVisibility(View.VISIBLE);
            waitingCount++;
        } else {
            waitingCount--;
            if (waitingCount == 0)
                pbLoading.setVisibility(View.INVISIBLE);
        }
    }

}
