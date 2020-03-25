package com.example.airpolito;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import androidx.fragment.app.Fragment;

import android.text.Html;
import android.text.Layout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;
import android.widget.TextView;


public class ProjectFragment extends Fragment {

    public ProjectFragment() {
        // Required empty public constructor
    }

    private WebView webView;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_project, container, false);

        webView = view.findViewById(R.id.wv_project_details);

        webView.loadUrl("file:///android_asset/project_details.html");
        // Inflate the layout for this fragment
        return view;
    }
}
